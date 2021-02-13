import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { TabFormComponent } from './tabForm.component';
import { TabViewModule } from 'primeng/tabview';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { ListboxModule } from 'primeng/listbox';
import { ButtonModule } from 'primeng/button';
import { ToolbarModule } from 'primeng/toolbar';
import { DialogModule } from 'primeng/dialog';
import { CheckboxModule } from 'primeng/checkbox';
import { SplitButtonModule } from 'primeng/splitbutton';
import { MenuModule } from 'primeng/menu';

import { MeaningFormModule } from '../meaningForm/meaningForm.module';
import { ChangesFormModule } from '../changesForm/changesForm.module';
import { SynonymModule } from '../synonym/synonym.module';
import { AntonymModule } from '../antonym/antonym.module';
import { ExpressionsModule } from '../expressions/expressions.module';
import { CollocationsModule } from '../collocation/collocations.module';
import { QualificatorModule } from '../qualificators/qualificator.module';

@NgModule({
  declarations: [TabFormComponent],
  imports: [
    BrowserModule,
    TabViewModule,
    InputTextModule,
    DropdownModule,
    FormsModule,
    ListboxModule,
    ButtonModule,
    SplitButtonModule,
    MenuModule,
    ToolbarModule,
    MeaningFormModule,
    SynonymModule,
    AntonymModule,
    ExpressionsModule,
    ChangesFormModule,
    CollocationsModule,
    DialogModule,
    CheckboxModule,
    QualificatorModule,
  ],
  exports: [TabFormComponent],
  providers: [],
  bootstrap: [TabFormComponent],
})
export class TabFormModule {}
