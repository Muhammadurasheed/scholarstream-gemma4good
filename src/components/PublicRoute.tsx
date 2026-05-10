import { Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { LoadingScreen } from "@/components/LoadingScreen";

interface PublicRouteProps {
    children: React.ReactNode;
    shouldRedirect?: boolean;
}

export const PublicRoute = ({ children, shouldRedirect = true }: PublicRouteProps) => {
    const { user, loading, isOnboardingComplete } = useAuth();

    if (loading) {
        return <LoadingScreen />;
    }

    if (user && shouldRedirect) {
        const destination = isOnboardingComplete() ? '/dashboard' : '/onboarding';
        console.log(`[PublicRoute] User logged in, redirecting to ${destination} (shouldRedirect: ${shouldRedirect})`);
        return <Navigate to={destination} replace />;
    }

    if (user) {
        console.log(`[PublicRoute] User logged in, but shouldRedirect is FALSE. Staying on current page.`);
    }

    // Not authenticated — render the public page (Login/SignUp/Landing)
    return <>{children}</>;
};
