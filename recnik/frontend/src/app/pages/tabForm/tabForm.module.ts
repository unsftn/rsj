import { NgModule } from '@angular/core';
import { TabFormComponent } from './tabForm.component';
import { TabViewModule } from 'primeng/tabview';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { FormsModule } from '@angular/forms';
import { ListboxModule } from 'primeng/listbox';
import { ButtonModule } from 'primeng/button';
import { GrammarInformationsModule } from '../grammarInformations/grammarInformations.module';
import { MeaningFormModule } from '../meaningForm/meaningForm.module';
import { SynonymModule } from '../synonym/synonym.module';
import { AntonymModule } from '../antonym/antonym.module';
import { ExpressionsModule } from '../expressions/expressions.module';
import { CollocationsModule } from '../collocation/collocations.module';

@NgModule({
  declarations: [TabFormComponent],
  imports: [
    TabViewModule,
    InputTextModule,
    DropdownModule,
    FormsModule,
    ListboxModule,
    ButtonModule,
    GrammarInformationsModule,
    MeaningFormModule,
    SynonymModule,
    AntonymModule,
    ExpressionsModule,
    CollocationsModule,
  ],
  exports: [TabFormComponent],
  providers: [],
  bootstrap: [TabFormComponent],
})
export class TabFormModule {}
