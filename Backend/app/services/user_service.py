def get_test_user() -> dict[str, str]:
    return {"message": "Users route is working"}


def get_current_user_profile(current_user: dict[str, str]) -> dict[str, str]:
    return {
        "email": current_user["email"],
        "message": "Authenticated user profile",
    }
