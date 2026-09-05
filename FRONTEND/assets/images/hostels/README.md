Place the hostel images here with the exact filenames used by the site and seed command:

- lurambi-outside.jpg
- lurambi-hall.jpg
- lurambi-room.jpg
- sichirai-outside.jpg
- sichirai-hall.jpg
- sichirai-room.jpg
- kefinco-outside.jpg
- kefinco-hall.jpg
- kefinco-room.jpg

Existing images detected in the repository root images folder:
 - `assets/images/lurambi.jpg`
 - `assets/images/sichirai.jpg`
 - `assets/images/kefinco.jpg`

The system will use these existing images as a fallback for each hostel (outside/hall/room) if the more specific filenames are not present. You may still add separate images per slot using the filenames above in this folder.

These are referenced as `/static/assets/images/hostels/<filename>` in the DB and in the frontend fallback data. After adding the images, collectstatic (or runserver in DEBUG) will serve them at `/static/assets/images/hostels/`.

Additionally, place the system-wide background image (the one you just provided) at:

- `FRONTEND/assets/images/global-bg.jpg`

This image is used as a subtle page background overlay so the entire site has a consistent look. The CSS uses a semi-transparent overlay to keep text readable.

To seed the database with these hostels (requires project dependencies installed):

```powershell
cd BACKEND
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_hostels
```

If `seed_hostels` fails with `ModuleNotFoundError: dj_database_url`, install that package (`pip install dj-database-url`) or ensure `requirements.txt` is installed into the active environment.
