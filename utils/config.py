# User system

PERMISSIONS = [
    'login', 'edit_self', # Manage account system
    'read_tickets', 'create_ticket', 'edit_ticket', 'conclude_ticket', # Ticket system
    'access_admin', 'create_user', 'edit_user', 'reset_password', 'delete_user' # Admin system
]

class Permissions:
    roles = dict()
    status = dict()
    @staticmethod
    def valide_hierarchy (author: str, affected: str):
        return Permissions.roles[author].hierarchy < Permissions.roles[affected].hierarchy
    
    @staticmethod
    def can_affect (perm: str, author, affected):
        can_role = Permissions.roles[author.role].permissions[perm]
        can_hierarchy = Permissions.valide_hierarchy(author.role, affected.role)
        can_status = perm not in Permissions.status[author.status].denied_permissions
        return can_role and can_hierarchy and can_status
    
    @staticmethod
    def can (author, perm: str):
        can_role = Permissions.roles[author.role].permissions[perm]
        can_status = perm not in Permissions.status[author.status].denied_permissions
        return can_role and can_status
        
class UserRole:
    def __init__(self, name: str, hierarchy: int, *permissions, all: bool = False):
        self.name = name
        self.hierarchy = hierarchy
        self.permissions = dict()
        self.__create_permissions(permissions, all)
        Permissions.roles[name] = self
        
    def __str__(self):
        return self.name.capitalize().replace('_', ' ')
        
    def __create_permissions (self, permissions, all):
        for permission in PERMISSIONS:
            if all or permission in permissions:
                self.permissions[permission] = True
            else:
                self.permissions[permission] = False
        
class UserStatus:
    def __init__(self, name: str, *denied_permissions, deny_all: bool = False):
        self.name = name
        if deny_all:
            self.denied_permissions = PERMISSIONS
        else:
            self.denied_permissions = denied_permissions
        Permissions.status[name] = self
        
    def __str__(self):
        return self.name.capitalize().replace('_', ' ')
            
# Ticket system

class TicketManagment:
    priorities = dict()
    status = dict()

class TicketPriority:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        TicketManagment.priorities[name] = self
        
    def __str__(self):
        return self.name.capitalize().replace('_', ' ')
        
class TicketStatus:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        TicketManagment.status[name] = self
    
    def __str__(self):
        return self.name.capitalize().replace('_', ' ')
    
# Aplications

# User roles

UserRole(
    'owner',
    0,
    all=True
)

UserRole(
    'administrator',
    1,
    all=True
)
UserRole(
    'default',
    2,
    'login', 'edit_self',
    'read_tickets', 'create_tickets', 'edit_tickets', 'conclude_tickets'
)

UserRole(
    'read_only',
    3,
    'login', 'edit_self',
    'read_tickets'
)

# User status

UserStatus(
    'active'
)

UserStatus(
    'suspended', 
    'read_tickets',
    'create_users', 'edit_users', 'reset_password', 'delete_users'
)

UserStatus(
    'inactive',
    deny_all = True
)

# Ticket priorities

TicketPriority(
    'high',
    '#fd151b'
)

TicketPriority(
    'medium',
    '#fc9e4f'
)

TicketPriority(
    'low',
    '#63a375'
)

# Ticket status

TicketStatus(
    'pending',
    '#63a375'
)

TicketStatus(
    'in_progress',
    '#fc9e4f'
)

TicketStatus(
    'finished',
    '#30323d'
)