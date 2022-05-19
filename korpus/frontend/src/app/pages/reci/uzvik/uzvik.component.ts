import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-uzvik',
  templateUrl: './uzvik.component.html',
  styleUrls: ['./uzvik.component.scss']
})
export class UzvikComponent implements OnInit {

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;

  constructor(
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
  }

  save(): void {
    
  }

}
