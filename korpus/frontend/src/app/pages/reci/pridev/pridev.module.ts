import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { TabViewModule } from 'primeng/tabview';
import { FieldsetModule } from 'primeng/fieldset';
import { CheckboxModule } from 'primeng/checkbox';
import { RippleModule } from 'primeng/ripple';
import { ButtonModule } from 'primeng/button';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { PridevComponent } from './pridev.component';
import { PossibleDupeModule } from '../../possible-dupe/possible-dupe.module';
import { AreYouSureModule } from '../../are-you-sure/are-you-sure.module';

const routes: Routes = [{ path: '', component: PridevComponent }]

@NgModule({
  declarations: [PridevComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    InputTextModule,
    TabViewModule,
    FieldsetModule,
    CheckboxModule,
    RippleModule,
    ButtonModule,
    MyToolbarModule,
    PossibleDupeModule,
    AreYouSureModule,
  ],
  exports: [RouterModule],
  bootstrap: [PridevComponent]
})
export class PridevModule { }
