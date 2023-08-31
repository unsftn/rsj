import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { TableModule } from 'primeng/table';
import { WordStatusComponent } from './word-status.component';

const routes: Routes = [{ path: '', component: WordStatusComponent }]

@NgModule({
  declarations: [
    WordStatusComponent
  ],
  imports: [
    CommonModule,
    TableModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [WordStatusComponent]
})
export class WordStatusModule { }
