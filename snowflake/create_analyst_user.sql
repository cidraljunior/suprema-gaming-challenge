begin;

set analyst_user     = 'aluizio';
set analyst_pass     = '_generate_this_';

create user identifier($analyst_user)
  password = identifier($analyst_pass)
  default_role = transformer
  default_warehouse = transforming
  must_change_password = true;

grant role transformer to user identifier($analyst_user);

commit;