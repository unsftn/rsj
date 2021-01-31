import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { SelectWordComponent } from './components/select-word/select-word.component';
import { FormSelectorComponent } from './components/form-selector/form-selector.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'tekst/:id',
    component: SelectWordComponent,
  },
  {
    path: 'rec',
    component: FormSelectorComponent,
  },
  {
    path: 'rec/:id',
    component: FormSelectorComponent,
  },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
