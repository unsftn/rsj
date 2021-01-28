import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './services/auth/auth.guard';
import { HomeComponent } from './pages/home/home.component';
import { TabFormComponent } from './pages/tabForm/tabForm.component';
import { LoginComponent } from './pages/login/login.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'add',
    component: TabFormComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' },
  },
  {
    path: 'edit/:id',
    component: TabFormComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' },
  },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
