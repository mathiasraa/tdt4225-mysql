from src.utils.data_load import get_trajectories_df, get_user_ids


def migrate():
    print("Migrating...")

    trajectories = get_trajectories_df("000")


if __name__ == "__main__":
    migrate()
