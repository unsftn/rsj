import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { ExpressionsComponent } from './expressions.component';

import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { AutoCompleteModule } from 'primeng/autocomplete';

@NgModule({
  declarations: [ExpressionsComponent],
  imports: [
    FormsModule,
    AutoCompleteModule,
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
