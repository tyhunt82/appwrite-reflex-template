"""Settings page state."""

import reflex as rx

from app.states.base import BaseState


class SettingsState(BaseState):
    """State for the settings page."""

    # Profile
    profile_name: str = "User"
    profile_email: str = "user@example.com"

    # Notifications
    email_alerts: bool = True
    push_notifications: bool = False
    weekly_digest: bool = True

    @rx.event
    def update_profile(self, form_data: dict):
        """Update profile information."""
        self.profile_name = form_data.get("name", self.profile_name)
        self.profile_email = form_data.get("email", self.profile_email)
        return rx.toast.success("Profile updated", position="bottom-right")

    @rx.event
    def toggle_email_alerts(self, value: bool):
        """Toggle email alerts setting."""
        self.email_alerts = value

    @rx.event
    def toggle_push_notifications(self, value: bool):
        """Toggle push notifications setting."""
        self.push_notifications = value

    @rx.event
    def toggle_weekly_digest(self, value: bool):
        """Toggle weekly digest setting."""
        self.weekly_digest = value
