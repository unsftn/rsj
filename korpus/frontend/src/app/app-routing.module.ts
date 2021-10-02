import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './services/auth/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { ImenicaComponent } from './pages/reci/imenica/imenica.component';
import { GlagolComponent } from './pages/reci/glagol/glagol.component';
import { PridevComponent } from './pages/reci/pridev/pridev.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'imenica/add',
    component: ImenicaComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'imenica/:id',
    component: ImenicaComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'glagol/add',
    component: GlagolComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'glagol/:id',
    component: GlagolComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'pridev/add',
    component: PridevComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'pridev/:id',
    component: PridevComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
