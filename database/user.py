from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import User, Base
from geopy.geocoders import Nominatim
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


geolocator = Nominatim(user_agent="ai_assistant")

def get_location_name(lat: float, lon: float) -> str:
    try:
        location = geolocator.reverse((lat, lon), language='en')
        if location and location.raw and 'address' in location.raw:
            address = location.raw['address']
            return (
                address.get('city')
                or address.get('town')
                or address.get('village')
                or address.get('municipality')
                or address.get('county')
                or "Unknown"
            )
        return "Unknown"
    except Exception as e:
        print(f"[Geocoding Error] {e}")
        return "Unknown"


async def init_user_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_or_update_user(user_id: str, first_name: str = None, last_name: str = None,
                                latitude: float = None, longitude: float = None):
    location_name = get_location_name(latitude, longitude) if latitude and longitude else None

    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                user.first_name = first_name or user.first_name
                user.last_name = last_name or user.last_name
                user.latitude = latitude or user.latitude
                user.longitude = longitude or user.longitude
                user.location = location_name or user.location
            else:
                user = User(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    latitude=latitude,
                    longitude=longitude,
                    location=location_name
                )
                session.add(user)
            print(user.location)
        await session.commit()

async def get_user_by_id(user_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.get(User, user_id)
        if result:
            return {
                "user_id": user_id,
                "first_name": result.first_name,
                "last_name": result.last_name,
                "latitude": result.latitude,
                "longitude": result.longitude,
                "location": result.location
            }
        return {
            "user_id": user_id,
            "first_name": None,
            "last_name": None,
            "latitude": None,
            "longitude": None,
            "location": None
        }