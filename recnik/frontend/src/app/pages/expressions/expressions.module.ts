import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';


import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';

import { ExpressionsComponent } from './expressions.component';
import { QualificatorModule } from '../qualificators/qualificator.module';
import { ConcordanceModule } from '../concordance/concordance.module';

@NgModule({
  declarations: [ExpressionsComponent],
  imports: [
    FormsModule,
    AutoCompleteModule,
    CommonModule,
    InputTextModule,
    InputTextareaModule,
    ButtonModule,
    DialogModule,
    TagModule,
    QualificatorModule,
    ConcordanceModule,
  ],
  exports: [ExpressionsComponent],
  providers: [],
  bootstrap: [ExpressionsComponent],
})
export class ExpressionsModule {}
