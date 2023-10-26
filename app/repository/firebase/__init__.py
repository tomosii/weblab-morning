from app.repository.firebase.commitment import CommitmentRepository
from app.repository.firebase.place import PlaceRepository
from app.repository.firebase.user import UserRepository
from app.repository.firebase.attendance import AttendanceRepository


commitment_repository = CommitmentRepository()
place_repository = PlaceRepository()
user_repository = UserRepository()
attendance_repository = AttendanceRepository()