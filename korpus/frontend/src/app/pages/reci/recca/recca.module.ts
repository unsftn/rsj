import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { InputTextModule } from 'primeng/inputtext';
import { MyToolbarModule } from '../../toolbar/toolbar.module';
import { ReccaComponent } from './recca.component';
import { PossibleDupeModule } from '../../possible-dupe/possible-dupe.module';

const routes: Routes = [{ path: '', component: ReccaComponent }]

@NgModule({
  declarations: [ReccaComponent],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule.forChild(routes),
    InputTextModule,
    MyToolbarModule,
    PossibleDupeModule,
  ],
  exports: [RouterModule],
  bootstrap: [ReccaComponent]
})
export class ReccaModule { }
