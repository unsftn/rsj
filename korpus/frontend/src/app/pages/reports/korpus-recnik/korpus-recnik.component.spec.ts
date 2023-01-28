import { ComponentFixture, TestBed } from '@angular/core/testing';

import { KorpusRecnikComponent } from './korpus-recnik.component';

describe('KorpusRecnikComponent', () => {
  let component: KorpusRecnikComponent;
  let fixture: ComponentFixture<KorpusRecnikComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ KorpusRecnikComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(KorpusRecnikComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
