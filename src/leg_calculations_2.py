import math


# The motor arm in a straight line to body of motor
# was set to a value of 500, so 0 degrees is not
# at a value of 0 but around 100.  there will be
# a small difference in how the motor was calibrated
# so you will need to check each motor using the
# ctrl.get_position_offset(motor_id)
MOTOR_OFFSET = 100
MOTOR_DEG = (749)/180  # 4.16111r

LEG_TRIANGLE_R = 156.62
LEG_TRIANGLE_S = 113.624
LEG_LENGTH = 193.494  # => math.sqrt(leg_triangle_r**2 + leg_triangle_s**2)
# calculated angle between LEG_TRIANGLE_R and LEG_OFFSET
# needed because the leg is not straight
LEG_OFFSET = 36

# distant from main spindle of each motor.
MOTOR_ONE_TO_MOTOR_TWO_DISTANCE = 60
MOTOR_TWO_TO_MOTOR_THREE_DISTANCE = 68

#  this is the maximum Positions that the leg can reach.
# from the spindle of motor 2 to the end of the leg
MAX_REACH_RADIUS = math.floor(
    MOTOR_TWO_TO_MOTOR_THREE_DISTANCE + LEG_LENGTH - 2)  # 261
# Any less than this is not possible, as the leg section
# will coliide with the the other leg section.
MIN_REACH_RADIUS = 148


def calculate_angles(x, y, z):
    """
    Calculates the angles of the legs given the
    x, y, z position of the leg.
    @ returns a tuple of angles in degrees
    """

    # calculate triangle alpha
    alpha_hypotenuse = clamp_leg_distance(math.sqrt(x**2 + z**2))
    alpha_angle_A = math.atan2(z, x)
    motor_1_angle = math.degrees(alpha_angle_A)

    # calculate triangle beta
    beta_x = alpha_hypotenuse - MOTOR_ONE_TO_MOTOR_TWO_DISTANCE
    beta_hypotenuse = math.sqrt(beta_x**2 + y**2)
    beta_angle_A = math.atan2(y, beta_x)
    # beta_angle_B = 180 - math.degrees(beta_angle_A) - 90

    # calculate triangle gamma
    gamma_angle_A = calc_angle_A(
        LEG_LENGTH, MOTOR_TWO_TO_MOTOR_THREE_DISTANCE, beta_hypotenuse)
    motor_2_angle = 180 - gamma_angle_A - beta_angle_A
    gamma_angle_C = calc_angle_C(
        LEG_LENGTH, MOTOR_TWO_TO_MOTOR_THREE_DISTANCE, beta_hypotenuse)
    motor_3_angle = 360 - 90 + gamma_angle_C + LEG_OFFSET

    return motor_1_angle, motor_2_angle, motor_3_angle


def calc_angle_A(side_r, side_s, side_t):
    """
    Calculate the angle A of the triangle
    see ref for details in main_1.py
    @ returns angle A in degrees
    """

    # cos A = (b2 + c2 - a2) / 2bc
    val = (side_s**2 + side_t**2 - side_r**2) / (2 * side_s * side_t)
    # use the math.acos function, this is the inverse cosine function
    # it returns radians

    # convert to degrees and return
    try:
        angle_A_radians = math.acos(val)
        return int(round(math.degrees(angle_A_radians)))
    except:
        # if the value is out of bounds, return -1
        if -1.0 > val > 1.0:
            print("Error: out of range -1 to 1 value was:", val)
        else:
            print("Error: calc_angle_a() value was:", val)
        return 90


def calc_angle_C(side_r, side_s, side_t):
    """
    Calculate the angle C of the triangle
    see ref for details in main_1.py
    @ returns angle C in degrees
    """
    # cos C = (a2 + b2 - c2) / 2ab
    return calc_angle_A(side_t, side_s, side_r)


def clamp_leg_distance(n):
    """
    Clamps the leg distance to the maximum/minimum
    leg distance.
    """
    print('clamp_motor_3_positions:', n)
    return max(min(MAX_REACH_RADIUS, n), MIN_REACH_RADIUS)
