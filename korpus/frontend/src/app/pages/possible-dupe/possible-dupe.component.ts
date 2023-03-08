import { Component, OnInit, EventEmitter, Input, Output } from '@angular/core';
import { RecService } from '../../services/reci';

@Component({
  selector: 'possible-dupe',
  templateUrl: './possible-dupe.component.html',
  styleUrls: ['./possible-dupe.component.scss']
})
export class PossibleDupeComponent implements OnInit {

  @Input() visible: boolean;
  @Output() visibleChanged: EventEmitter<boolean> = new EventEmitter<boolean>();

  @Output() yes: EventEmitter<boolean> = new EventEmitter<boolean>();

  @Output() no: EventEmitter<boolean> = new EventEmitter<boolean>();

  @Input() dupes: any[];

  constructor(
    private recService: RecService,
  ) {
    this.dupes = [];
    this.visible = false;
  }

  ngOnInit(): void {}

  yesClicked(): void {
    this.yes.emit(true);
    this.visible = true;
  }

  noClicked(): void {
    this.no.emit(true);
    this.visible = false;
  }

  editLink(wordId: number, wordType: number): any[] {
    return this.recService.getEditRouterLink(wordId, wordType);
  }
}
