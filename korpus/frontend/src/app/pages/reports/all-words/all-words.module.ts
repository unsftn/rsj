import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { TableModule } from 'primeng/table';
import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';
import { TabViewModule } from 'primeng/tabview';
import { InputTextModule } from 'primeng/inputtext';
import { AllWordsComponent } from './all-words.component';

const routes: Routes = [{ path: '', component: AllWordsComponent }]

@NgModule({
  declarations: [AllWordsComponent],
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    DropdownModule,
    ButtonModule,
    TabViewModule,
    InputTextModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule],
  bootstrap: [AllWordsComponent]
})
export class AllWordsModule { }
