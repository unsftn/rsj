import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DropdownModule } from 'primeng/dropdown';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ButtonModule } from 'primeng/button';
import { InputNumberModule } from 'primeng/inputnumber';
import { FieldsetModule } from 'primeng/fieldset';
import { DialogModule } from 'primeng/dialog';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { RippleModule } from 'primeng/ripple';
import { ConcordanceComponent } from './concordance.component';

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
    AutoCompleteModule,
    RippleModule
  ],
  exports: [ConcordanceComponent],
  providers: [],
  bootstrap: [ConcordanceComponent],
})
export class ConcordanceModule {}
