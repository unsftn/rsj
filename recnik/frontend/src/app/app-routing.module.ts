import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PublikacijaListComponent } from './pages/publikacije/publikacija-list/publikacija-list.component';
import { PublikacijaComponent } from './pages/publikacije/publikacija/publikacija.component';
import { AllComponent } from './pages/review/all/all.component';
import { AuthGuard } from './services/auth/auth.guard';
import { HomeComponent } from './pages/home/home.component';
import { TabFormComponent } from './pages/tabForm/tabForm.component';
import { LoginComponent } from './pages/login/login.component';
import { RendersComponent } from './pages/renders/renders/renders.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { PersonComponent } from './pages/review/person/person.component';

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
    path: 'renders',
    component: RendersComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'edit/:id',
    component: TabFormComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' },
  },
  {
    path: 'pubs',
    component: PublikacijaListComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'pubs/add',
    component: PublikacijaComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' },
  },
  {
    path: 'pubs/edit/:id',
    component: PublikacijaComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' },
  },
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'review/by-person',
    component: PersonComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'review/alphabetical',
    component: AllComponent,
    canActivate: [AuthGuard],
  },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
