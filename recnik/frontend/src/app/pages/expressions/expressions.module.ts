import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { ExpressionsComponent } from './expressions.component';

import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { InputTextareaModule } from 'primeng/inputtextarea';

@NgModule({
  declarations: [ExpressionsComponent],
  imports: [
    FormsModule,
    DropdownModule,
    CommonModule,
    InputTextModule,
    InputTextareaModule,
    ButtonModule,
  ],
  exports: [ExpressionsComponent],
  providers: [],
  bootstrap: [ExpressionsComponent],
})
export class ExpressionsModule {}
