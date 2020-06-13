import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UIRouterModule } from '@uirouter/angular';

import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';



@NgModule({
  declarations: [
    LoginComponent,
    RegisterComponent
  ],
  imports: [
    CommonModule,
    UIRouterModule
  ]
})
export class UserModule { }
