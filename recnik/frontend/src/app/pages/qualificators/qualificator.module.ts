import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { QualificatorComponent } from './qualificator.component';

import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';
import { ListboxModule } from 'primeng/listbox';
import { HttpClientModule } from '@angular/common/http';
import { TooltipModule } from 'primeng/tooltip';

@NgModule({
  declarations: [QualificatorComponent],
  imports: [
    FormsModule,
    DropdownModule,
    CommonModule,
    ButtonModule,
    ListboxModule,
    TooltipModule,
    HttpClientModule,
  ],
  exports: [QualificatorComponent],
  providers: [],
  bootstrap: [QualificatorComponent],
})
export class QualificatorModule {}
