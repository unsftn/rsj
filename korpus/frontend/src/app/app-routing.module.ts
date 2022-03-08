import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PubListComponent } from './pages/pub-list/pub-list.component';
import { PubTextComponent } from './pages/pub-text/pub-text.component';
import { PublicationComponent } from './pages/publication/publication.component';
import { AuthGuard } from './services/auth/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { ImenicaComponent } from './pages/reci/imenica/imenica.component';
import { GlagolComponent } from './pages/reci/glagol/glagol.component';
import { PridevComponent } from './pages/reci/pridev/pridev.component';
import { ProcessStepComponent } from './pages/pub-import/process-step/process-step.component';
import { SelectFilesComponent } from './pages/pub-import/select-files/select-files.component';

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
    path: 'publikacije',
    component: PubListComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'publikacija/add',
    component: PublicationComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' },
  },
  {
    path: 'publikacija/:id',
    component: PublicationComponent,
    canActivate: [AuthGuard],
    data: { mode: 'edit' },
  },
  {
    path: 'publikacija/:pid/fragment/:fid',
    component: PubTextComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'obrada/:pid/korak/:step',
    component: ProcessStepComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'obrada/:pid/datoteke',
    component: SelectFilesComponent,
    canActivate: [AuthGuard],
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
