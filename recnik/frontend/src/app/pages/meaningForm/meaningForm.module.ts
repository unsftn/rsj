import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ButtonModule } from 'primeng/button';
import { FieldsetModule } from 'primeng/fieldset';

import { ConcordanceModule } from '../concordance/concordance.module';
import { SubmeaningModule } from '../submeaning/submeaning.module';
import { QualificatorModule } from '../qualificators/qualificator.module';
import { ExpressionsModule } from '../expressions/expressions.module';

import { MeaningFormComponent } from './meaningForm.component';

@NgModule({
  declarations: [MeaningFormComponent],
  imports: [
    DropdownModule,
    CommonModule,
    InputTextModule,
    InputTextareaModule,
    FormsModule,
    ButtonModule,
    FieldsetModule,
    ConcordanceModule,
    SubmeaningModule,
    QualificatorModule,
    ExpressionsModule,
  ],
  exports: [MeaningFormComponent],
  providers: [],
  bootstrap: [MeaningFormComponent],
})
export class MeaningFormModule {}
