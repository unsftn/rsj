import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './services/auth/auth.guard';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { SelectWordComponent } from './components/select-word/select-word.component';
import { FormSelectorComponent } from './components/form-selector/form-selector.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'tekst/:id',
    component: SelectWordComponent,
    //canActivate: [AuthGuard]
  },
  {
    path: 'add',
    component: FormSelectorComponent,
    //canActivate: [AuthGuard]
  },
  {
    path: 'edit/:vrsta/:id',
    component: FormSelectorComponent,
    //canActivate: [AuthGuard]
  },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
