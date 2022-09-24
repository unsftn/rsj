import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { TableModule } from 'primeng/table';
import { MojeReciComponent } from './moje-reci.component';

const routes: Routes = [{ path: '', component: MojeReciComponent }]

@NgModule({
  declarations: [MojeReciComponent],
  imports: [
    CommonModule,
    TableModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [MojeReciComponent]
})
export class MojeReciModule { }
