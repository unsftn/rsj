import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { TableModule } from 'primeng/table';
import { BrojUnetihReciComponent } from './broj-unetih-reci.component';

const routes: Routes = [{ path: '', component: BrojUnetihReciComponent }]

@NgModule({
  declarations: [BrojUnetihReciComponent],
  imports: [
    CommonModule,
    TableModule,
    RouterModule.forRoot(routes),
  ],
  exports: [RouterModule],
  bootstrap: [BrojUnetihReciComponent]
})
export class BrojUnetihReciModule { }
