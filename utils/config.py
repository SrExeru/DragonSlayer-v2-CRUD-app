priority_levels = {
    'low': '#63A375',
    'medium': '#FC9E4F',
    'high': '#FD151B'
}

def get_priority (raw_level: str):
    level = raw_level.strip().lower()
    if level not in priority_levels:
        raise ValueError('Invalid priority')
    return level

role_levels = {
    'owner': 3,
    'administrator': 2,
    'default': 1,
    'read_only': 0 
}

def get_role (raw_role: str):
    level = raw_role.strip().lower().replace(' ', '_')
    if level not in role_levels:
        raise ValueError('Invalid role')
    return level