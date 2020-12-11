import { NgModule } from '@angular/core';
import { GrammarInformationsComponent } from './grammarInformations.component';
import { DropdownModule } from 'primeng/dropdown';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';

@NgModule({
  declarations: [GrammarInformationsComponent],
  imports: [DropdownModule, CommonModule, InputTextModule, InputTextareaModule],
  exports: [GrammarInformationsComponent],
  providers: [],
  bootstrap: [GrammarInformationsComponent],
})
export class GrammarInformationsModule {}
