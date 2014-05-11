#Configuration du projet
cmake_minimum_required(VERSION 2.8)
project(raspi)

set(EXECUTABLE_OUTPUT_PATH bin/)
set(EXEC_NAME raspi)

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
