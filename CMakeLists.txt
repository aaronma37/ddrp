cmake_minimum_required(VERSION 2.8.3)
project(ddrp)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  std_msgs
  geometry_msgs
  rospy
  message_generation
)



#catkin_python_setup()


###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)


add_message_files(
	FILES
	Environment.msg
	Objective.msg
	RegionObjectiveState.msg
	Region.msg
	Agent.msg
	Waypoint.msg
	Task.msg)
                                        #PoseWithName.msg

#add_message_files( DIRECTORY msg FILES  pathData.msg )
                                        #PoseWithName.msg

generate_messages(
  DEPENDENCIES
  std_msgs
#  geometry_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES polyhedral_terrains_demo
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
   CATKIN_DEPENDS message_runtime
)




###########
## Build ##
###########

#file(GLOB_RECURSE HEADER_FILES include/*.h)


 catkin_install_python(PROGRAMS
    src/main_ros.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  )
#  catkin_install_python(PROGRAMS
#    src/agent_standard.py
#    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#  )

#  catkin_install_python(PROGRAMS
#    src/draw.py
#    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#  )








