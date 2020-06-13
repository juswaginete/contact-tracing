import { ContentOnly } from 'src/app/commons/utils/layout.utils';

import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';

export const USERS_STATES: object[] = [
  {
    name: 'login',
    url: '/login',
    views: ContentOnly(LoginComponent),
    // params: {next: window.location.pathname}
  },
  {
    name: 'register',
    url: '/register',
    views: ContentOnly(RegisterComponent),
    // params: {next: window.location.pathname}
  },
  // {
  //   name: 'logout',
  //   url: '/logout',
  //   onEnter: Disconnect
  // }
];
