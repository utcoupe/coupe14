cmake_minimum_required(VERSION 2.8)

#Configuration du projet
project(Visio)
set(EXECUTABLE_OUTPUT_PATH bin/)
set(EXEC_NAME visio)
find_package( OpenCV REQUIRED )
SET(CMAKE_CXX_FLAGS "-std=c++11")
SET(CMAKE_CXX_FLAGS_TIME "-DTIMEBENCH=true")

#Configurationdel'exécutable

file(
	GLOB_RECURSE
	source_files
	src/*
)

add_executable(
	${EXEC_NAME}
	${source_files}
)

include_directories( ${OpenCV_INCLUDE_DIRS} )
target_link_libraries( ${EXEC_NAME} ${OpenCV_LIBS} )
