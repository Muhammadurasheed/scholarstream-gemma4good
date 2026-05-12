"""
Gemma 4 ReAct Agent (V3) — Hackathon Native Implementation
Architected for Gemini 4 Good. All Gemini logic has been purged.

This agent uses Gemma 4 (27B) as the reasoning core to execute tool calls,
analyze opportunities, and provide empathetic guidance to students.
"""
import json
import asyncio
import structlog
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.models import UserProfile
from app.database import db
from app.config import settings
from app.services.gemma_service import gemma_service
from app.services.cortex.navigator import scout
from app.services.personalization_engine import personalization_engine

logger = structlog.get_logger()

class GemmaReActChatService:
    """
    Native Gemma 4 Agent with full reasoning and ranking capabilities.
    """

    def __init__(self):
        # Tools defined using OpenAI/Vertex style schema
        self.tool_definitions = [
            {
                "name": "search_database",
                "description": "Search the local database for scholarships, hackathons, and bounties using structured filters.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "enum": ["scholarship", "hackathon", "bounty", "grant", "any"]},
                        "min_amount": {"type": "integer", "description": "Minimum amount in USD"},
                        "limit": {"type": "integer", "description": "Max results to return"}
                    }
                }
            },
            {
                "name": "vector_search",
                "description": "Semantic search to find opportunities by meaning/context (e.g. 'funding for female engineers')",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "dispatch_scout",
                "description": "Dispatch autonomous web crawlers (Cortex Sentinel) to find FRESH online opportunities.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Specific search query for the crawler"}
                    },
                    "required": ["query"]
                }
            }
        ]
        
        self.tools_map = {
            'search_database': self._tool_search_database,
            'vector_search': self._tool_vector_search,
            'dispatch_scout': self._tool_dispatch_scout
        }

    async def chat(self, user_id: str, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Manual ReAct loop for Gemma 4 via Vertex AI MaaS"""
        current_date = datetime.now().strftime("%B %d, %Y")
        profile = context.get('user_profile', {})
        
        system_instruction = f"""You are the ScholarStream AI, powered natively by Gemma 4.
Current Date: {current_date}
User Profile: {json.dumps(profile)}

Tone: Professional, warm, globally inclusive, and highly empathetic. 
Rules:
1. Always check the database first.
2. If the user wants fresh data or local results are thin, dispatch a scout.
3. Acknowledge user constraints (GPA, major, location) with empathy."""

        thinking_process = ["[Reasoning] Analyzing request with Gemma 4 Reasoning..."]
        
        final_text = ""
        found_opportunities = []
        
        try:
            # ReAct Loop
            for turn in range(3):
                # We feed the current turn context to Gemma
                # In a real ReAct loop, we would append tool results to the conversation
                response_json = await gemma_service.generate_content_async(
                    prompt=message, 
                    system_instruction=system_instruction,
                    tools=self.tool_definitions
                )
                
                message_data = response_json["choices"][0]["message"]
                
                # Handle Thinking
                if "thinking" in message_data:
                    thinking_process.append(f"[Thinking] {message_data['thinking']}")
                
                # Check for Tool Calls
                tool_calls = message_data.get("tool_calls")
                if tool_calls:
                    for tc in tool_calls:
                        fn_name = tc["function"]["name"]
                        fn_args = json.loads(tc["function"]["arguments"])
                        
                        thinking_process.append(f"[Action] Executing `{fn_name}` for lead discovery.")
                        
                        if fn_name in self.tools_map:
                            result = await self.tools_map[fn_name](user_id, **fn_args)
                            if isinstance(result, list):
                                found_opportunities.extend(result)
                                thinking_process.append(f"[Observation] Found {len(result)} potential matches.")
                            else:
                                thinking_process.append(f"[Observation] Tool executed successfully.")
                            
                            # Append to message for the next model turn
                            message += f"\n[Observation from {fn_name}]: {json.dumps(result[:5])}"
                        else:
                            thinking_process.append(f"[Warning] Tool `{fn_name}` not available in this environment.")
                else:
                    final_text = message_data.get("content", "")
                    break
            
            # Final Synthesis if turn loop finished without final answer
            if not final_text:
                thinking_process.append("[Synthesis] Finalizing my advice based on Gemma 4 reasoning.")
                summary_prompt = f"Summarize your findings for the student based on our discovery work. Results found: {len(found_opportunities)}"
                summary_resp = await gemma_service.generate_content_async(prompt=summary_prompt, system_instruction=system_instruction)
                final_text = summary_resp["choices"][0]["message"]["content"]

            # Post-process opportunities (Ranking & Diversity)
            ranked_opps = await self._rank_opportunities(found_opportunities, profile)

            return {
                'message': final_text,
                'thinking_process': "\n\n".join(thinking_process),
                'opportunities': ranked_opps[:12],
                'suggestions': self._generate_suggestions(final_text, ranked_opps),
                'actions': self._generate_actions(ranked_opps)
            }

        except Exception as e:
            logger.error("Gemma Chat Loop failed", error=str(e))
            return {
                'message': "I apologize, but I encountered an error while thinking with Gemma 4. Please try again.",
                'thinking_process': "\n".join(thinking_process + [f"[Error] {str(e)}"]),
                'opportunities': [],
                'suggestions': [],
                'actions': []
            }

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TOOL IMPLEMENTATIONS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    async def _tool_search_database(self, user_id, type="any", min_amount=0, limit=10):
        opps = await db.get_all_scholarships()
        now_str = datetime.now().strftime("%Y-%m-%d")
        filtered = []
        for o in opps:
            o_dict = o.model_dump() if hasattr(o, 'model_dump') else o
            if o_dict.get('deadline') and o_dict.get('deadline') < now_str: continue
            if type != "any" and type.lower() not in self._infer_type(o_dict): continue
            if (o_dict.get('amount') or 0) < (min_amount or 0): continue
            filtered.append(o_dict)
        return filtered[:limit]

    async def _tool_vector_search(self, user_id, query, limit=10):
        from app.services.vectorization_service import vectorization_service
        vec = await vectorization_service.vectorize_query(query)
        results = await db.semantic_search(vec, limit=limit)
        return [r.model_dump() if hasattr(r, 'model_dump') else r for r in results]

    async def _tool_dispatch_scout(self, user_id, query):
        asyncio.create_task(scout.execute_mission(query))
        return {"status": "scouts_dispatched", "target": query}

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LOGIC HELPERS (Gemma Optimized)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    async def _rank_opportunities(self, opps: List[Dict], profile: Dict) -> List[Dict]:
        user_profile_obj = None
        try: user_profile_obj = UserProfile(**profile) if profile else None
        except Exception: pass

        results = []
        seen_ids = set()
        for opp in opps:
            if not opp or opp.get('id') in seen_ids: continue
            seen_ids.add(opp['id'])
            
            score = 50
            if user_profile_obj:
                try: score = await personalization_engine.calculate_personalized_score(opp, user_profile_obj)
                except Exception: score = opp.get('match_score', 50)
            
            results.append({**opp, 'match_score': int(score), 'type': self._infer_type(opp)})

        results.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        return results

    def _infer_type(self, opp) -> str:
        combined = f"{' '.join(opp.get('tags', []) or [])} {opp.get('description', '')} {opp.get('name', '')}".lower()
        if 'hackathon' in combined: return 'hackathon'
        if 'bounty' in combined: return 'bounty'
        if 'grant' in combined: return 'grant'
        return 'scholarship'

    def _generate_suggestions(self, text: str, opps: List[Dict]) -> List[str]:
        return ["How do I apply?", "Find more hackathons", "Filter by amount"]

    def _generate_actions(self, opportunities: List[Dict]) -> List[Dict]:
        if not opportunities: return []
        return [{
            'type': 'navigate',
            'label': '🎯 View Top Match',
            'data': {'path': f"/opportunity/{opportunities[0]['id']}"}
        }]

# Global Instance
gemma_chat_service = GemmaReActChatService()
