import { Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { LoadingScreen } from "@/components/LoadingScreen";

interface PublicRouteProps {
    children: React.ReactNode;
}

export const PublicRoute = ({ children }: PublicRouteProps) => {
    const { user, loading, isOnboardingComplete } = useAuth();

    if (loading) {
        return <LoadingScreen />;
    }

    if (user) {
        // Route based on onboarding status — never blindly send to /dashboard
        const destination = isOnboardingComplete() ? '/dashboard' : '/onboarding';
        return <Navigate to={destination} replace />;
    }

    // Not authenticated — render the public page (Login/SignUp/Landing)
    return <>{children}</>;
};
