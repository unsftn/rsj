import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { SynonymComponent } from './synonym.component';

import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';

@NgModule({
  declarations: [SynonymComponent],
  imports: [FormsModule, DropdownModule, CommonModule, ButtonModule],
  exports: [SynonymComponent],
  providers: [],
  bootstrap: [SynonymComponent],
})
export class SynonymModule {}
