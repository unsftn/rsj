import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ButtonModule } from 'primeng/button';
import { FieldsetModule } from 'primeng/fieldset';
import { DialogModule } from 'primeng/dialog';
import { TabViewModule } from 'primeng/tabview';
import { RippleModule } from 'primeng/ripple';
import { ConcordanceModule } from '../concordance/concordance.module';
import { SubmeaningModule } from '../submeaning/submeaning.module';
import { QualificatorModule } from '../qualificators/qualificator.module';
import { ExpressionsModule } from '../expressions/expressions.module';
import { MeaningFormComponent } from './meaningForm.component';
import { ShortCollocationModule } from '../short-collocation/short-collocation.module';
import { SynonymModule } from '../synonym/synonym.module';
import { AntonymModule } from '../antonym/antonym.module';

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
    DialogModule,
    TabViewModule,
    RippleModule,
    ConcordanceModule,
    SubmeaningModule,
    QualificatorModule,
    ExpressionsModule,
    ShortCollocationModule,
    SynonymModule,
    AntonymModule,
  ],
  exports: [MeaningFormComponent],
  providers: [],
  bootstrap: [MeaningFormComponent],
})
export class MeaningFormModule {}
