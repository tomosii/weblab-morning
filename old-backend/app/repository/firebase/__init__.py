from app.repository.firebase.commitment import CommitmentRepository
from app.repository.firebase.place import PlaceRepository
from app.repository.firebase.user import UserRepository
from app.repository.firebase.attendance import AttendanceRepository
from app.repository.firebase.point import PointRepository
from app.repository.firebase.trivia import TriviaRepository


commitment_repository = CommitmentRepository()
place_repository = PlaceRepository()
user_repository = UserRepository()
attendance_repository = AttendanceRepository()
point_repository = PointRepository()
trivia_repository = TriviaRepository()
