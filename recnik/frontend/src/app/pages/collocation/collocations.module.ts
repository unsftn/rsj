import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { CollocationsComponent } from './collocations.component';

import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';
import { InputTextareaModule } from 'primeng/inputtextarea';

@NgModule({
  declarations: [CollocationsComponent],
  imports: [
    FormsModule,
    DropdownModule,
    CommonModule,
    ButtonModule,
    InputTextareaModule,
  ],
  exports: [CollocationsComponent],
  providers: [],
  bootstrap: [CollocationsComponent],
})
export class CollocationsModule {}
