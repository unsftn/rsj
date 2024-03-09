import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { PredlogComponent } from './predlog.component';
import { PossibleDupeModule } from '../../possible-dupe/possible-dupe.module';
import { AreYouSureModule } from '../../are-you-sure/are-you-sure.module';

const routes: Routes = [{ path: '', component: PredlogComponent }]

@NgModule({
  declarations: [PredlogComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    InputTextModule,
    ButtonModule,
    MyToolbarModule,
    PossibleDupeModule,
    AreYouSureModule,
  ],
  exports: [RouterModule],
  bootstrap: [PredlogComponent]
})
export class PredlogModule { }
