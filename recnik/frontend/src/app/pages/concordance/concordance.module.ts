import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ConcordanceComponent } from './concordance.component';

import { DropdownModule } from 'primeng/dropdown';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ButtonModule } from 'primeng/button';
import { InputNumberModule } from 'primeng/inputnumber';
import { FieldsetModule } from 'primeng/fieldset';
import { DialogModule } from 'primeng/dialog';

@NgModule({
  declarations: [ConcordanceComponent],
  imports: [
    DropdownModule,
    CommonModule,
    InputTextModule,
    InputTextareaModule,
    FormsModule,
    ButtonModule,
    InputNumberModule,
    FieldsetModule,
    DialogModule,
  ],
  exports: [ConcordanceComponent],
  providers: [],
  bootstrap: [ConcordanceComponent],
})
export class ConcordanceModule {}
