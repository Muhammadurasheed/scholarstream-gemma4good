
import json
import time
from typing import Dict, List, Any, Optional
import structlog
from upstash_redis import Redis
from app.config import settings

logger = structlog.get_logger()

class DiscoveryPulseService:
    """
    Real-time mission tracking with Distributed (Redis) and Local (Memory) support.
    Provides transparency into what the Sentinel and AI Refinery are doing.
    """
    
    PULSE_KEY = "cortex:discovery:pulse"
    MISSION_TTL = 3600 # 1 hour
    
    def __init__(self):
        self.redis = None
        self.memory_pulse: Dict[str, str] = {} # Fallback for local stability
        self.circuit_open = False
        self.circuit_reset_time = 0
        self.failure_count = 0
        self.MAX_FAILURES = 3
        self.CIRCUIT_TIMEOUT = 300 # 5 minutes disable on failure
        
        if settings.upstash_redis_rest_url and settings.upstash_redis_rest_token:
            try:
                self.redis = Redis(
                    url=settings.upstash_redis_rest_url,
                    token=settings.upstash_redis_rest_token
                )
                # Test connection immediately
                self.redis.ping()
            except Exception as e:
                logger.warning("Pulse: Redis connection failed, falling back to Memory Vault", error=str(e))
                self.redis = None
                
    async def update_mission(self, mission_id: str, target: str, status: str = "active"):
        """Broadcast mission status to the world"""
        label = ""
        if status == "active":
            if "DNA" in target or "Analyzing" in target or "Geolocation" in target:
                label = target # Keep system DNA logs as is
            elif "Scanning" in target or "Patrolling" in target:
                label = target
            else:
                label = f"Sentinel is patrolling {target}"
        else:
            label = f"Mission {status.capitalize()}"

        pulse_data = {
            "mission_id": mission_id,
            "target": target,
            "status": status,
            "timestamp": time.time(),
            "label": label
        }
        
        # 1. Update Memory (Immediate & Reliable Fallback)
        self.memory_pulse[mission_id] = json.dumps(pulse_data)
        
        # 2. Update Redis (Distributed)
        if self.redis and not self._circuit_open():
            try:
                self.redis.hset(self.PULSE_KEY, mission_id, json.dumps(pulse_data))
                self.redis.expire(self.PULSE_KEY, self.MISSION_TTL)
                logger.debug("Pulse: Mission Synchronized to Redis", mission=target)
            except Exception as e:
                self._record_failure()

    def complete_mission(self, mission_id: str, found_count: int = 0):
        """Mark a mission as completed and report yield"""
        raw = self.memory_pulse.get(mission_id)
        if raw:
            data = json.loads(raw)
            data["status"] = "completed"
            data["found_count"] = found_count
            data["completed_at"] = time.time()
            data["label"] = f"Mission Complete: {found_count} items found on {data.get('target')}"
            
            # Update Memory
            self.memory_pulse[mission_id] = json.dumps(data)
            
            # Update Redis
            if self.redis and not self._circuit_open():
                try:
                    self.redis.hset(self.PULSE_KEY, mission_id, json.dumps(data))
                except:
                    pass

    def get_active_missions(self) -> List[Dict[str, Any]]:
        """Retrieve all active/recently completed missions"""
        all_missions_raw = {}
        
        # 1. Try Redis first for distributed data
        if self.redis and not self._circuit_open():
            try:
                all_missions_raw = self.redis.hgetall(self.PULSE_KEY)
            except:
                self._record_failure()
        
        # 2. Fallback/Merge with Memory
        if not all_missions_raw:
            all_missions_raw = self.memory_pulse
        
        if not all_missions_raw: return []
        
        missions = []
        now = time.time()
        for mid, raw in all_missions_raw.items():
            try:
                data = json.loads(raw)
                # Clean up old memory pulse
                if data.get("status") == "completed" and (now - data.get("completed_at", 0)) > 300:
                    if mid in self.memory_pulse: del self.memory_pulse[mid]
                    continue
                missions.append(data)
            except:
                continue
        
        return sorted(missions, key=lambda x: x.get('timestamp', 0), reverse=True)

    def _circuit_open(self) -> bool:
        """Check if circuit is open (disabled)"""
        if self.circuit_open:
            if time.time() > self.circuit_reset_time:
                self.circuit_reset_time = 0
                self.circuit_open = False
                self.failure_count = 0
                logger.info("Pulse: Circuit Breaker RESET. Retrying Redis.")
                return False
            return True
        return False

    def _record_failure(self):
        """Record a failure and trip circuit if threshold reached"""
        self.failure_count += 1
        if self.failure_count >= self.MAX_FAILURES:
            self.circuit_open = True
            self.circuit_reset_time = time.time() + self.CIRCUIT_TIMEOUT
            logger.error("Pulse: Circuit Breaker TRIPPED. Redis disabled for 5 minutes to prevent spam.")

# Global instance
discovery_pulse = DiscoveryPulseService()
