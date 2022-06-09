# REACHDOC_BACKEND_FASTAPI
This is an API and Backend code for a medical product called REACHDOC. This project is created with python's FastApi web framework. It  implements user-based access control on two levels; 
1) Admin: This user is a superuser and is authorized to create, delete and Update Doctors and patients but isn't authorized to perform C.R.U.D operations on other admins.  
2) Patient and Doctor: These are regular users and they are authorized to only login and update their information/profile for a period of time until verification is implemented,  profile updating will not be possible anymore after doctor and patient verification is implemented.
