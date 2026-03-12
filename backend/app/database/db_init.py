from app.database.mongodb import get_db

async def init_collections():
    db = get_db()
    collections = await db.list_collection_names()

    required = ["users", "projects", "tasks", "schedules", "productivity_logs"]
    for col in required:
        if col not in collections:
            await db.create_collection(col)
            print(f"Created collection: {col}")

    # Indexes
    await db.users.create_index("email", unique=True)
    await db.projects.create_index("creator_id")
    await db.tasks.create_index("project_id")
    await db.schedules.create_index([("user_id", 1), ("project_id", 1)])
    await db.productivity_logs.create_index("user_id")
    print("Indexes created")
