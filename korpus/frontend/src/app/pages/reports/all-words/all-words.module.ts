import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { TableModule } from 'primeng/table';
import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';
import { AllWordsComponent } from './all-words.component';

const routes: Routes = [{ path: '', component: AllWordsComponent }]

@NgModule({
  declarations: [AllWordsComponent],
  imports: [
    CommonModule,
    TableModule,
    DropdownModule,
    ButtonModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [AllWordsComponent]
})
export class AllWordsModule { }
