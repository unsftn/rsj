import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './services/auth/auth.guard';
import { EditGuard } from './services/auth/edit.guard';
import { VolunteerGuard } from './services/auth/volunteer.guard';

const routes: Routes = [
  {
    path: '',
    loadChildren: () => import('./pages/home/home.module').then((m) => m.HomeModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'search',
    loadChildren: () => import('./pages/search/search.module').then((m) => m.SearchModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'profil',
    loadChildren: () => import('./pages/profile/profile.module').then((m) => m.ProfileModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'login',
    loadChildren: () => import('./pages/login/login.module').then((m) => m.LoginModule),
  },
  {
    path: 'pretraga',
    loadChildren: () => import('./pages/advanced-search/advanced-search.module').then((m) => m.AdvancedSearchModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'imenica/add',
    loadChildren: () => import('./pages/reci/imenica/imenica.module').then((m) => m.ImenicaModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'imenica/:id',
    loadChildren: () => import('./pages/reci/imenica/imenica.module').then((m) => m.ImenicaModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'glagol/add',
    loadChildren: () => import('./pages/reci/glagol/glagol.module').then((m) => m.GlagolModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'glagol/:id',
    loadChildren: () => import('./pages/reci/glagol/glagol.module').then((m) => m.GlagolModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'pridev/add',
    loadChildren: () => import('./pages/reci/pridev/pridev.module').then((m) => m.PridevModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'pridev/:id',
    loadChildren: () => import('./pages/reci/pridev/pridev.module').then((m) => m.PridevModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'predlog/add',
    loadChildren: () => import('./pages/reci/predlog/predlog.module').then((m) => m.PredlogModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'predlog/:id',
    loadChildren: () => import('./pages/reci/predlog/predlog.module').then((m) => m.PredlogModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'recca/add',
    loadChildren: () => import('./pages/reci/recca/recca.module').then((m) => m.ReccaModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'recca/:id',
    loadChildren: () => import('./pages/reci/recca/recca.module').then((m) => m.ReccaModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'uzvik/add',
    loadChildren: () => import('./pages/reci/uzvik/uzvik.module').then((m) => m.UzvikModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'uzvik/:id',
    loadChildren: () => import('./pages/reci/uzvik/uzvik.module').then((m) => m.UzvikModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'veznik/add',
    loadChildren: () => import('./pages/reci/veznik/veznik.module').then((m) => m.VeznikModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'veznik/:id',
    loadChildren: () => import('./pages/reci/veznik/veznik.module').then((m) => m.VeznikModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'zamenica/add',
    loadChildren: () => import('./pages/reci/zamenica/zamenica.module').then((m) => m.ZamenicaModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'zamenica/:id',
    loadChildren: () => import('./pages/reci/zamenica/zamenica.module').then((m) => m.ZamenicaModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'broj/add',
    loadChildren: () => import('./pages/reci/broj/broj.module').then((m) => m.BrojModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'broj/:id',
    loadChildren: () => import('./pages/reci/broj/broj.module').then((m) => m.BrojModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'prilog/add',
    loadChildren: () => import('./pages/reci/prilog/prilog.module').then((m) => m.PrilogModule),
    canActivate: [AuthGuard],
    data: { mode: 'add' }
  },
  {
    path: 'prilog/:id',
    loadChildren: () => import('./pages/reci/prilog/prilog.module').then((m) => m.PrilogModule),
    canActivate: [AuthGuard],
    data: { mode: 'edit' }
  },
  {
    path: 'izvori',
    loadChildren: () => import('./pages/pub-list/pub-list.module').then((m) => m.PubListModule),
    canActivate: [EditGuard],
  },
  {
    path: 'import/:pid',
    loadChildren: () => import('./pages/pub-import/importer.module').then((m) => m.ImporterModule),
    canActivate: [EditGuard],
  },
  {
    path: 'odluke',
    loadChildren: () => import('./pages/reports/all-words/all-words.module').then((m) => m.AllWordsModule),
    canActivate: [VolunteerGuard],
  },
  {
    path: 'izvestaji/korpus-recnik',
    loadChildren: () => import('./pages/reports/korpus-recnik/korpus-recnik.module').then((m) => m.KorpusRecnikModule),
    canActivate: [EditGuard],
  },
  {
    path: 'izvestaji/broj-unetih-reci',
    loadChildren: () => import('./pages/reports/broj-unetih-reci/broj-unetih-reci.module').then((m) => m.BrojUnetihReciModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'izvestaji/moje-reci',
    loadChildren: () => import('./pages/reports/moje-reci/moje-reci.module').then((m) => m.MojeReciModule),
    canActivate: [AuthGuard],
    data: { mode: 'self' }
  },
  {
    path: 'izvestaji/reci-korisnika/:userID',
    loadChildren: () => import('./pages/reports/moje-reci/moje-reci.module').then((m) => m.MojeReciModule),
    canActivate: [AuthGuard],
    data: { mode: 'other' }
  },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
