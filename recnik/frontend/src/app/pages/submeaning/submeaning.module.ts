import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SubmeaningComponent } from './submeaning.component';

import { DropdownModule } from 'primeng/dropdown';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ButtonModule } from 'primeng/button';
import { ConcordanceModule } from '../concordance/concordance.module';
import { QualificatorModule } from '../qualificators/qualificator.module';
import { ExpressionsModule } from '../expressions/expressions.module';
import { FieldsetModule } from 'primeng/fieldset';

@NgModule({
  declarations: [SubmeaningComponent],
  imports: [
    DropdownModule,
    CommonModule,
    InputTextModule,
    InputTextareaModule,
    FormsModule,
    ButtonModule,
    ConcordanceModule,
    QualificatorModule,
    FieldsetModule,
    ExpressionsModule,
  ],
  exports: [SubmeaningComponent],
  providers: [],
  bootstrap: [SubmeaningComponent],
})
export class SubmeaningModule {}
