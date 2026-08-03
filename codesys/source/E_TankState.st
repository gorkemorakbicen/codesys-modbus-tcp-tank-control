{attribute 'qualified_only'}
{attribute 'strict'}
TYPE E_Tankstate :
(
    INIT,
    FILLING,
    DRAINING,
    MANUAL_IDLE,
    MANUAL_FILLING,
    MANUAL_DRAINING,
    MANUAL_CONFLICT,
    COMM_LOSS,
    COMM_FAULT
);
END_TYPE
