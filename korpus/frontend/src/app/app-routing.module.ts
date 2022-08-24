import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PubListComponent } from './pages/pub-list/pub-list.component';
import { PubTextComponent } from './pages/pub-text/pub-text.component';
import { PublicationComponent } from './pages/publication/publication.component';
import { AuthGuard } from './services/auth/auth.guard';
import { EditGuard } from './services/auth/edit.guard';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { ProcessStepComponent } from './pages/pub-import/process-step/process-step.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { ImenicaComponent } from './pages/reci/imenica/imenica.component';
import { GlagolComponent } from './pages/reci/glagol/glagol.component';
import { PridevComponent } from './pages/reci/pridev/pridev.component';
import { PredlogComponent } from './pages/reci/predlog/predlog.component';
import { ReccaComponent } from './pages/reci/recca/recca.component';
import { UzvikComponent } from './pages/reci/uzvik/uzvik.component';
import { VeznikComponent } from './pages/reci/veznik/veznik.component';
import { ZamenicaComponent } from './pages/reci/zamenica/zamenica.component';
import { BrojComponent } from './pages/reci/broj/broj.component';
import { PrilogComponent } from './pages/reci/prilog/prilog.component';
import { AdvancedSearchComponent } from './pages/advanced-search/advanced-search.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'profil',
    component: ProfileComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'pretraga',
    component: AdvancedSearchComponent,
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
    canActivate: [EditGuard],
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
    canActivate: [EditGuard],
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
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'predlog/add',
    component: PredlogComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'predlog/:id',
    component: PredlogComponent,
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'recca/add',
    component: ReccaComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'recca/:id',
    component: ReccaComponent,
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'uzvik/add',
    component: UzvikComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'uzvik/:id',
    component: UzvikComponent,
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'veznik/add',
    component: VeznikComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'veznik/:id',
    component: VeznikComponent,
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'zamenica/add',
    component: ZamenicaComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'zamenica/:id',
    component: ZamenicaComponent,
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'broj/add',
    component: BrojComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'broj/:id',
    component: BrojComponent,
    canActivate: [EditGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'prilog/add',
    component: PrilogComponent,
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'prilog/:id',
    component: PrilogComponent,
    canActivate: [EditGuard],
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
    canActivate: [EditGuard],
    data: { mode: 'edit' },
  },
  {
    path: 'publikacija/:pid/fragment/:fid',
    component: PubTextComponent,
    canActivate: [EditGuard],
  },
  {
    path: 'obrada/:pid/korak/:step',
    component: ProcessStepComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'import/:pid',
    // component: SelectFilesComponent,
    loadChildren: () => import('./pages/pub-import/importer.module').then((m) => m.ImporterModule),
    canActivate: [EditGuard],
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
