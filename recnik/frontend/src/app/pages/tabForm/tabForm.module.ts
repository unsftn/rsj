import { NgModule } from '@angular/core';
import { TabFormComponent } from './tabForm.component';
import { TabViewModule } from 'primeng/tabview';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { FormsModule } from '@angular/forms';
import { ListboxModule } from 'primeng/listbox';
import { ButtonModule } from 'primeng/button';
import { GrammarInformationsModule } from '../grammarInformations/grammarInformations.module';

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
  ],
  exports: [TabFormComponent],
  providers: [],
  bootstrap: [TabFormComponent],
})
export class TabFormModule {}